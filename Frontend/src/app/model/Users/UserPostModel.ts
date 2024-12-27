export class UserPost {
  public userNickname: string;
  public userEmail: string;
  public userAge: number;

  constructor(userNickname: string, userEmail: string, userAge: number) {
    this.userNickname = userNickname;
    this.userEmail = userEmail;
    this.userAge = userAge;
  }

  public getUserNickname(): string {
    return this.userNickname;
  }

  public getUserEmail(): string {
    return this.userEmail;
  }

  public getUserAge(): number {
    return this.userAge;
  }
}

export class UserPostFlaskFormat {
  nick_name: string;
  email: string;
  age: number;

  constructor(nickname: string, email: string, age: number) {
    this.nick_name = nickname;
    this.email = email;
    this.age = age;
  }
}
