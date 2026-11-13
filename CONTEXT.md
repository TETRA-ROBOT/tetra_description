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
