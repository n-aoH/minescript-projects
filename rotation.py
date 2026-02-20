from system.lib import minescript as ms
import time, math, random
from dataclasses import dataclass

"""
All credit goes to @Jones in the minescript discord for this library.

I couldn't find an official repo for it, so I forked it and added look_at(x, y, z).

"""


@dataclass
class HumanLookConfig:
    min_speed: float = 35.0
    max_speed: float = 260.0
    min_angle: float = 5.0
    max_angle: float = 140.0
    min_duration: float = 0.045
    max_duration: float = 0.75
    max_curve_intensity: float = 0.14
    base_overshoot: float = 0.012
    max_overshoot: float = 0.040
    overshoot_bias: float = 0.55
    jitter_deg: float = 0.04
    jitter_smooth: float = 0.85
    jitter_scale_small_moves: float = 0.35
    target_hz: float = 120.0
    step_jitter: float = 0.22
    micro_settle_deg: float = 0.06
    micro_settle_steps: int = 3
    deadzone_deg: float = 0.05
    pitch_min: float = -89.9
    pitch_max: float = 89.9
    no_overshoot_deg: float = 8.0
    no_curve_deg: float = 10.0
    lock_cone_deg: float = 0.85
    lock_time: float = 0.08
    lock_servo_speed: float = 110.0
    urgent_speed_mult_max: float = 1.8
    urgent_duration_mult_min: float = 0.55
    urgent_curve_scale: float = 0.25
    urgent_no_curve_deg: float = 22.0
    urgent_no_overshoot_deg: float = 18.0
    urgent_lock_cone_deg: float = 0.60
    urgent_lock_time: float = 0.05
    urgent_lock_servo_speed: float = 220.0

CFG = HumanLookConfig()

def _wrap_deg(a):
    return (a + 180.0) % 360.0 - 180.0

def _clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def _hypot2(a, b):
    return math.sqrt(a * a + b * b)

def _min_jerk(t):
    t3 = t * t * t
    t4 = t3 * t
    t5 = t4 * t
    return 10.0 * t3 - 15.0 * t4 + 6.0 * t5

def _map_speed(ang, cfg):
    if ang <= cfg.min_angle:
        return cfg.min_speed * (0.6 + 0.8 * (ang / max(1e-6, cfg.min_angle)))
    if ang >= cfg.max_angle:
        return cfg.max_speed
    r = (ang - cfg.min_angle) / (cfg.max_angle - cfg.min_angle)
    r = r ** 0.7
    return cfg.min_speed + (cfg.max_speed - cfg.min_speed) * r

def _lateral_curve(ang, cfg):
    r = _clamp((ang - cfg.min_angle) / (cfg.max_angle - cfg.min_angle), 0.0, 1.0)
    return cfg.max_curve_intensity * (r ** 1.2)

def _overshoot_frac_raw(ang, cfg):
    r = _clamp((ang - cfg.min_angle) / (cfg.max_angle - cfg.min_angle), 0.0, 1.0)
    base = cfg.base_overshoot + (cfg.max_overshoot - cfg.base_overshoot) * (r ** 0.9)
    return base * (0.75 + 0.5 * random.random())

def _sleep_step(dt, cfg):
    jitter = 1.0 + cfg.step_jitter * (random.random() - 0.5) * 2.0
    time.sleep(max(0.001, dt * jitter))

def _move_segment(a0, b0, dy, dp, duration, lateral_frac, cfg, target_yaw, target_pitch, tolerance, jitter_state=None, jitter_scale_override=None):
    hz = cfg.target_hz
    dt = 1.0 / hz
    steps = max(1, int(duration * hz))
    ang = max(_hypot2(dy, dp), 1e-6)
    ux, uy = dy / ang, dp / ang
    px, py = -uy, ux
    if jitter_state is None:
        jitter_state = {"jy": 0.0, "jp": 0.0}
    jy, jp = jitter_state["jy"], jitter_state["jp"]
    base_scale = cfg.jitter_scale_small_moves if ang < 12.0 else 1.0
    if jitter_scale_override is not None:
        base_scale = _clamp(jitter_scale_override, 0.0, 1.0)
    for i in range(1, steps + 1):
        t = i / steps
        s = _min_jerk(t)
        byaw = dy * s
        bpitch = dp * s
        bell = math.sin(math.pi * s)
        lat = lateral_frac * ang * bell
        lyaw = px * lat
        lpitch = py * lat
        jy = cfg.jitter_smooth * jy + (1.0 - cfg.jitter_smooth) * (random.random() - 0.5)
        jp = cfg.jitter_smooth * jp + (1.0 - cfg.jitter_smooth) * (random.random() - 0.5)
        jitter_yaw = cfg.jitter_deg * jy * base_scale
        jitter_pitch = cfg.jitter_deg * jp * base_scale
        yaw = _wrap_deg(a0 + byaw + lyaw + jitter_yaw)
        pitch = _clamp(b0 + bpitch + lpitch + jitter_pitch, cfg.pitch_min, cfg.pitch_max)

        
        if _hypot2(_wrap_deg(target_yaw - yaw), target_pitch - pitch) <= tolerance:
            
            ms.player_set_orientation(target_yaw, target_pitch)
            break
        
        ms.player_set_orientation(yaw, pitch)
        _sleep_step(dt, cfg)
    jitter_state["jy"] = jy
    jitter_state["jp"] = jp
    return jitter_state

def _urgency_value(urgent):
    if isinstance(urgent, bool):
        return 1.0 if urgent else 0.0
    try:
        return _clamp(float(urgent), 0.0, 1.0)
    except Exception:
        return 0.0

def look(target_yaw, target_pitch, cfg=CFG, urgent=0.0, tolerance=None):
    u = _urgency_value(urgent)
    a, b = ms.player_orientation()
    dy = _wrap_deg(target_yaw - a)
    tp = _clamp(target_pitch, cfg.pitch_min, cfg.pitch_max)
    dp = tp - b
    ang = _hypot2(dy, dp)
    tol = tolerance if tolerance is not None else cfg.deadzone_deg
    if ang < tol:
        return
    no_curve_thresh = (1.0 - u) * cfg.no_curve_deg + u * cfg.urgent_no_curve_deg
    no_overshoot_thresh = (1.0 - u) * cfg.no_overshoot_deg + u * cfg.urgent_no_overshoot_deg
    no_curve = ang <= no_curve_thresh
    no_overshoot = ang <= no_overshoot_thresh
    wrap_band = (1.0 - u) * 18.0 + u * 24.0
    near_wrap = abs(abs(dy) - 180.0) <= wrap_band
    speed = _map_speed(ang, cfg) * (1.0 + u * (cfg.urgent_speed_mult_max - 1.0))
    base_T = _clamp(ang / max(1e-6, speed), cfg.min_duration, cfg.max_duration)
    duration = base_T * (1.0 - u * (1.0 - cfg.urgent_duration_mult_min)) * (0.9 + 0.2 * random.random())
    if no_curve:
        lateral_frac = 0.0
    else:
        lateral_frac = _lateral_curve(ang, cfg) * (0.85 + 0.3 * random.random())
        lateral_frac *= (1.0 - u * (1.0 - cfg.urgent_curve_scale))
    if no_overshoot or near_wrap:
        overshoot_y = 0.0
        overshoot_p = 0.0
    else:
        over_frac = _overshoot_frac_raw(ang, cfg) * (1.0 - 0.85 * u)
        axis_mix = cfg.overshoot_bias if abs(dy) >= abs(dp) else (cfg.overshoot_bias * 0.8)
        overshoot_y = dy * over_frac * (axis_mix + 0.22 * (random.random() - 0.5))
        overshoot_p = dp * over_frac * ((1.0 - axis_mix) + 0.22 * (random.random() - 0.5))
    main_jitter_scale = 1.0 - 0.85 * u
    jitter_state = _move_segment(a, b, dy + overshoot_y, dp + overshoot_p, duration, lateral_frac, cfg, target_yaw, target_pitch, tol, jitter_state=None, jitter_scale_override=main_jitter_scale)
    corr_dy = -overshoot_y
    corr_dp = -overshoot_p
    corr_ang = _hypot2(corr_dy, corr_dp)
    if corr_ang >= tol * 0.5:
        corr_speed = max(cfg.min_speed * 0.7, _map_speed(corr_ang, cfg) * (0.6 + 0.25 * u))
        corr_T = _clamp(corr_ang / corr_speed, cfg.min_duration * (0.55 - 0.10 * u), cfg.min_duration * (1.45 - 0.25 * u))
        _move_segment(_wrap_deg(a + dy + overshoot_y), _clamp(b + dp + overshoot_p, cfg.pitch_min, cfg.pitch_max), corr_dy, corr_dp, corr_T, lateral_frac * 0.35, cfg, target_yaw, target_pitch, tol, jitter_state=jitter_state, jitter_scale_override=0.25 * (1.0 - u))
    sy, sp = ms.player_orientation()
    rem_dy = _wrap_deg(target_yaw - sy)
    rem_dp = _clamp(target_pitch, cfg.pitch_min, cfg.pitch_max) - sp
    rem_ang = _hypot2(rem_dy, rem_dp)
    if rem_ang > tol * 0.6:
        lock_speed = (1.0 - u) * cfg.lock_servo_speed + u * cfg.urgent_lock_servo_speed
        snap_T = _clamp(rem_ang / lock_speed, cfg.min_duration * (0.45 - 0.10 * u), cfg.min_duration * (0.9 - 0.15 * u))
        _move_segment(sy, sp, rem_dy, rem_dp, snap_T, 0.0, cfg, target_yaw, target_pitch, tol, jitter_state=jitter_state, jitter_scale_override=0.0)
    lock_deadline = time.time() + ((1.0 - u) * cfg.lock_time + u * cfg.urgent_lock_time)
    lock_cone = (1.0 - u) * cfg.lock_cone_deg + u * cfg.urgent_lock_cone_deg
    lock_speed = (1.0 - u) * cfg.lock_servo_speed + u * cfg.urgent_lock_servo_speed
    while time.time() < lock_deadline:
        cy, cp = ms.player_orientation()
        edy = _wrap_deg(target_yaw - cy)
        edp = _clamp(target_pitch, cfg.pitch_min, cfg.pitch_max) - cp
        eang = _hypot2(edy, edp)
        if eang <= max(lock_cone, tol):
            break
        nib_T = _clamp(eang / lock_speed, cfg.min_duration * 0.30, cfg.min_duration * 0.55)
        _move_segment(cy, cp, edy, edp, nib_T, 0.0, cfg, target_yaw, target_pitch, tol, jitter_state=jitter_state, jitter_scale_override=0.0)
    for k in range(max(1, int(cfg.micro_settle_steps - round(1.0 * u)))):
        sy, sp = ms.player_orientation()
        jitter = cfg.micro_settle_deg * (0.6 ** k)
        nudge_y = (random.random() - 0.5) * 2.0 * jitter
        nudge_p = (random.random() - 0.5) * 2.0 * jitter * 0.7
        _move_segment(sy, sp, nudge_y, nudge_p, cfg.min_duration * (0.32 - 0.06 * u), 0.0, cfg, target_yaw, target_pitch, tol, jitter_scale_override=0.25 * (1.0 - u))
        
# Down here is contributions from @No, to be able to look at a BlockPos

def grounddist(x,z,x2,z2):
     return ((x-x2) ** 2 + (z-z2) ** 2) ** .5

def get_axes(x, y, z):
     ax = x   #actual x, actual y, actual z
     ay = y - 1.7
     az = z 
     px, py, pz = ms.get_player().position

     pitch = math.atan2(py-ay,grounddist(px,pz,ax,az))

     yaw = math.atan2(pz-az,px-ax)
     
     
     return (math.degrees(yaw) + 90, math.degrees(pitch))

def look_at(x,y,z, **kwargs):
    """
    Passes through:
    cfg=CFG, urgent=0.0, tolerance=None

    urgent: makes it faster
    
    """
    look(*get_axes(x,y,z), **kwargs)
