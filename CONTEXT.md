# tetra_description - AI Agent Context

## 개요
TETRA 로봇과 Herkulex 서보 장치의 URDF(xacro)·메쉬·RViz 설정 패키지입니다.
`tetra_config`의 브링업 런치가 `FindPackageShare('tetra_description')`로 xacro 를 읽어 `robot_state_publisher`에 넘깁니다.

## 패키지 맵

| 패키지 | 내용 |
|---|---|
| `tetra_description` | 로봇 본체. `launch/tetra_{m,h,s,sm,mh}_description.launch.py`, `urdf/tetra.xacro`·`base.urdf.xacro`와 모델별 폴더(`tetra_s/`, `tetra_sm/`, `tetra_mh/`, `tetra_edu/`, `tetraDS/`) |
| `herkulex_description` | Pan/Tilt, 로봇 팔 등 Herkulex 서보 장치 (`urdf/herkulex_*.xacro`) |

## AI 에이전트 주의사항
1. **`urdf/legacy_archive/`는 빌드·런치 어디에서도 참조하지 않습니다.** 예전 모델 참고용이니 수정 대상이 아닙니다.
2. 링크·조인트 이름을 바꾸면 TF 를 쓰는 곳이 모두 영향을 받습니다: Nav2/SLAM 파라미터(`tetra_config`), 센서 드라이버 frame_id, 웹 API 의 로봇 외곽선(`TetraSingleManagement/tetra-single-api/src/lib/robot/robot-footprint.ts`).
3. 단위는 URDF 표준(m, rad)입니다.
4. `urdf/tetra.xacro` 는 거의 모든 모델 브링업이 읽습니다. 한 모델에만 있는 부품은 xacro 인자로 막아 두고 그 모델 브링업만 켭니다 (예: M 후면 초음파 `m_rear_sonar:=true`).
5. **MH + 로봇팔**: `urdf/tetra_mh/tetra_rb10.xacro` = MH 몸체 + Rainbow RB10(`rbpodo_description`, 이 레포 밖) + 몸통 장착(rb_joint).
   Autonics 카메라(`mh_assy_camera`)는 xacro 인자 `autonics_camera_mount`(gripper: 팔 끝단 원 `tcp` 기준 `autonics_gripper_xyz/rpy`, pantilt: 팬틸트 브래킷, none)로 옮긴다.
   `herkulex_description/urdf/test.xacro` 가 같은 인자를 pantilt 기본으로 선언하고, 드라이버가 내는 `camera_link` 를 카메라 몸체에 잇는다.
6. **모델마다 자기 폴더의 `base.urdf.xacro` 를 읽는다.** 공용 `urdf/base.urdf.xacro` 는 M 몸체다. 2026-08 모델별 패키지를 합칠 때 S·SM 이 공용(M) base 를 읽게 남아
   S·SM 화면에 M 몸체가 보였고, S 2D·3D, SM 3D 브링업은 `robot_state_publisher_node()` 를 인자 없이 불러 M URDF 전체(라이다·카메라 위치까지 M 값)를 냈다. 지금은 `xacro_folder='tetra_s'|'tetra_sm'`.
   자기 base 의 캐스터 이름은 `l_rear_caster_*` 다 (M 은 `rear_caster_*`, RViz 표시 목록에만 쓰임). `tetra_3d_bringup_mh` 도 같은 문제였고 지금은 `tetra_mh` 를 읽는다.
   SM 의 `livox_frame`(MID360, SM 3D 브링업)은 실측값이 없어 S 와 같은 자리다. MH 의 `livox_frame` 도 실측값이 없어 S 와 같은 자리다.
7. **바닥 높이 `floor_drop`** (H 0.015, EDU·SM 0.025): `base_joint` 는 0.1 m 인데 바퀴 반지름이 H 0.085, EDU·SM 0.075 라 메쉬가 떠 보였다.
   base_joint 를 바꾸면 base_link 기준 센서 높이(3D 라이다 높이 필터 등)가 같이 바뀌어 TF 는 그대로 두고 메쉬 origin 만 내렸다. 그래서 base_link·바퀴 프레임은 실제 바퀴축보다 그만큼 높다.
   센서 높이를 바닥에서 실측하면 base_joint 를 바퀴 반지름으로 고치고 floor_drop 을 0, 센서 joint z 를 실측값에 맞춘다.
8. M 앞 라이다(TiM571, `laser`)는 `meshes/sick_tim_5xx.stl`(sick_scan_xd, Apache-2.0, `meshes/sick_tim_5xx.NOTICE.md`)로 그린다. 원점이 광학 중심이라 오프셋 없이 붙인다.
