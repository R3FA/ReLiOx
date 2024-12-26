export class UserPatch {
  public id: number;
  public username: string;
  public email: string;
  public age: number;

  constructor(id: number, username: string, email: string, age: number) {
    this.id = id;
    this.username = username;
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
