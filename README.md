# westagram-backend
## 초기 세팅 및 진행 방법
- 원하는 directory 이동 후 해당 repo를 clone 받아주세요.
- main 브랜치를 기준으로 `feature/이름-구현중인기능` 브랜치를 만들어주세요. (ex. `feature/kyunghun-initail-seting`, `feature/kyunhun-signup`)
    > 현업에서 브랜치에 본인 이름을 삽입하지 않고, 기능 단위로만 생성합니다. 실제 프로젝트에서는 브랜치에 자신의 이름을 작성하지 않도록 주의해주세요.
- 새롭게 생성한 브랜치로 이동후 `students` 폴더에 본인 이름의 폴더를 만들어주세요. 
(ex. `students` > `kyunghun-kang` 폴더 생성)
- `$ django-admin startproject westagram .` 명령어로 Django 프로젝트를 생성해주세요.
- https://www.notion.so/wecode/Django-6dbc3a4f5594433d974e0ed3c8d22858 링크를 참고해서 프로젝트 초기 설정을 진행해주세요.
- 이렇게 폴더 및 파일 조 세팅이 완료되면 작업을 진행합니다.
- 작업 중간 중간 commit 잘 남기고, 완료 시 origin main로 push 후 PR(pull request) 까지 완료해주세요.
- 리뷰 내용은 반영해서 코드 수정하고 다시 push 해주세요.
- 해당 branch의 label이 Accepted로 바뀌면 미션 완료입니다.

## 리뷰 코멘트를 반영한 뒤 진행 방법
- 멘토님들이 남긴 코멘트를 잘 읽고 브랜치에서 코드를 수정해주세요.
- 수정 하신 후 다시 add, commit, push 해주세요.
- 수정이 완료된 코멘트에는 `Resolve conversation` 버튼을 눌러주세요.

## 필수 구현 항목
- [User] 회원가입 엔드포인트(SignUp): 
    - 회원가입 로직 작성
    - url 연결
    - 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 반환
    - 회원가입 성공시 {"message": "SUCCESS"}, status code 201 return

- [User] 로그인 엔드포인트(SignIn):
    - 로그인 로직 작성
    - url 연결
    - 로그인 성공시 {"message": "SUCCESS"}, status code 200 return
    - 계정 잘 못 입력시 {"message": "INVALID_USER"}, status code 401 에러 return
    - 비밀번호 잘 못 입력시 {"message": "INVALID_USER"}, status code 401 에러 return

## 보너스 구현 사항
- [Posting] 특정 유저의 게시물에 댓글 달기 엔드포인트
    - 유저 아이디, 댓글 내용, 최초 댓글 단 시간, 수정 시간 포함될 것
- [Posting] 게시물 올리기

## 위코드 파이썬 코딩 컨벤션
- Import 순서
    1. Python 모듈
    2. Django 모듈
    3. 내가 만든 모듈

    ```python
    import json
    # 간격 한 줄 
    from django.db      import models
    # 간격 한 줄
    from user.models    import User
    from product.models import Drink        
    ```

- Code Align
    - `import` 를 기준으로 정렬해주세요
    - `Class`나 `Function` 내부에서 선언하는 변수들의 경우 `=`을 기준으로 정렬해줍니다.
    ```python
    from user.models    import User
    from product.models import Drink

    class Product(models.Model):
        product_code = models.CharField(max_length=100, null=True)
        name         = models.CharField(max_length=50, null=True)
        price        = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    ```
- 보다 자세한 규칙은 노션에서 확인해주세요
    - [파이썬 코딩 컨벤션](https://www.notion.so/wecode/wecode-Python-Coding-Convention-0bd47a6018634454b9ee1e27984cb83a)
구
