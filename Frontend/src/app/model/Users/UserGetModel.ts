export class UserGet {
  private id: number;
  private nickname: string;
  private email: string;
  private age: number;

  constructor(id: number, nickname: string, email: string, age: number) {
    this.id = id;
    this.nickname = nickname;
    this.email = email;
    this.age = age;
  }

  public getUserID(): number {
    return this.id;
  }

  public getUserNickname(): string {
    return this.nickname;
  }

  public getUserEmail(): string {
    return this.email;
  }

  public getUserAge(): number {
    return this.age;
  }
}

export class UserGetFlaskFormat {
  public id: number;
  public nick_name: string;
  public email: string;
  public age: number;

  constructor(id: number, nick_name: string, email: string, age: number) {
    this.id = id;
    this.nick_name = nick_name;
    this.email = email;
    this.age = age;
  }
}
