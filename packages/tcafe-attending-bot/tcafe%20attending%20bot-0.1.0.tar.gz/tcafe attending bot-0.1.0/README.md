# TCafe attending bot

## 아이디 설정

__OS 별 [`XDG_DATA_DIRS`](https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html)이 해당하는 곳에 설정__ (복수 설정 가능)

---

`Linux`의 경우

1. `/home/<$HOME>/.local/share/tcafe`
2. `/usr/local/share/tcafe`
3. `/usr/share/tcafe`

---

해당 디렉토리들에 `accounts.json` 이름으로 다음의 템플릿을 참고하여 내용을 작성

```json
[
    {
        "id": "ididid",
        "password": "password"
    },
    {
        "id": "ididid2",
        "password": "password2"
    }
]
```

## 실행

패키지 설치 후

```bash
tcafe_attending_bot
```