import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserPost } from './model/Users/UserPostModel';
import { UserService } from './service/user.service';
import { FormsModule } from '@angular/forms';
import { UserGet, UserGetFlaskFormat } from './model/Users/UserGetModel';
import { UserPostFlaskFormat } from './model/Users/UserPostModel';
import { UserPatch, UserPatchFlaskFormat } from './model/Users/UserPatchModel';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [CommonModule, FormsModule],
})
export class AppComponent implements OnInit {
  // HTML Titles
  public navBarTitle: string = 'ReLiOx - Gaming Session Manager';
  public sideBarUserPanelTitle: string = 'User Panel';
  public sideBarChooseUserTitle: string = 'Choose';
  public formNicknameTitle: string = 'Nickname';
  public formEmailTitle: string = 'Email';
  public formAgeTitle: string = 'Age';
  public createGameSessionButtionTitle: string = 'Create Gaming Session';
  public currentUser: string = '';

  // Bool
  public isUserChosen: boolean = false;

  // CRUD objects
  public userGetAllData: UserGet[] = [];
  public userPostData: UserPostFlaskFormat = new UserPostFlaskFormat('', '', 0);
  public userPatchData: UserPatch = new UserPatch(0, '', '', 0);
  public userData: UserGet = new UserGet(0, '', '', 0);

  // Response types
  public userDeleteAlertType: 'success' | 'danger' | null = null;
  public userDeleteAlertMessage: string = '';

  public userCreateAlertType: 'success' | 'danger' | null = null;
  public userCreateAlertMessage: string = '';

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.GetAllUsers();
  }

  private refreshPage(): void {
    setTimeout(() => {
      window.location.reload();
    }, 2000);
  }

  public closeButton(): void {
    this.userDeleteAlertType = null;
    this.userCreateAlertType = null;
    this.userDeleteAlertMessage = '';
    this.userCreateAlertMessage = '';
  }

  public sendUserDetails(
    user: UserGet,
    isForPatch: boolean
  ): UserPatch | UserGet {
    if (isForPatch) {
      return (this.userPatchData = new UserPatch(
        user.getUserID(),
        user.getUserNickname(),
        user.getUserEmail(),
        user.getUserAge()
      ));
    } else {
      return (this.userData = new UserGet(
        user.getUserID(),
        user.getUserNickname(),
        user.getUserEmail(),
        user.getUserAge()
      ));
    }
  }

  // User endpoints
  public GetAllUsers(): UserGet[] {
    this.userService.GetAll().subscribe({
      next: (users: UserGetFlaskFormat[]) => {
        this.userGetAllData = users.map(
          (user) => new UserGet(user.id, user.nick_name, user.email, user.age)
        );
      },
      error: (error) => {
        console.error(error?.error?.message);
      },
    });
    return [];
  }

  public CreateUser(userPostData: UserPostFlaskFormat): void {
    this.userService.Create(userPostData).subscribe({
      next: (createdUser: UserPostFlaskFormat) => {
        let newUser = new UserPost(
          createdUser.nick_name,
          createdUser.email,
          createdUser.age
        );
        this.userCreateAlertType = 'success';
        this.userCreateAlertMessage = `User with nickname ${newUser.getUserNickname()} has been CREATED successfully!`;
        this.refreshPage();
      },
      error: (error) => {
        this.userCreateAlertType = 'danger';
        this.userCreateAlertMessage =
          error?.error?.message || 'An error occurred!';
      },
    });
  }

  public PatchUser(user: UserPatch): void {
    let patchedUser = new UserPatchFlaskFormat(
      user.nickname,
      user.email,
      user.age
    );

    this.userService.Patch(user.id, patchedUser).subscribe({
      next: () => {
        this.userCreateAlertType = 'success';
        this.userCreateAlertMessage = `User with id ${user.id} has been PATCHED successfully!`;
        this.refreshPage();
      },
      error: (error) => {
        this.userCreateAlertType = 'danger';
        this.userCreateAlertMessage =
          error?.error?.message || 'An error occurred!';
      },
    });
  }

  public DeleteUser(userID: number, username: string): void {
    this.userService.Delete(userID).subscribe({
      next: () => {
        this.userDeleteAlertType = 'success';
        this.userDeleteAlertMessage = `User with nickname ${username} has been deleted successfully!`;
        this.refreshPage();
      },
      error: (error) => {
        this.userDeleteAlertType = 'danger';
        this.userDeleteAlertMessage =
          error?.error?.message || 'An error occurred!';
      },
    });
  }

  // User Gaming Sessions Endpoints
  public ChooseUser(): void {
    this.currentUser = `User:${this.userData.getUserNickname()}`;
    this.isUserChosen = true;
  }
}
