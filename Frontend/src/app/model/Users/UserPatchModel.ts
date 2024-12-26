export class UserPatch {
  public id: number;
  public nickname: string;
  public email: string;
  public age: number;

  constructor(id: number, nickname: string, email: string, age: number) {
    this.id = id;
    this.nickname = nickname;
    this.email = email;
    this.age = age;
  }
}

export class UserPatchFlaskFormat {
  public nick_name: string;
  public email: string;
  public age: number;

  constructor(nick_name: string, email: string, age: number) {
    this.nick_name = nick_name;
    this.email = email;
    this.age = age;
  }
}
