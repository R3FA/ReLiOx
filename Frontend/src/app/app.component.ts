import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserPost } from './model/Users/UserPostModel';
import { UserService } from './service/user.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [CommonModule, FormsModule],
})
export class AppComponent {
  public navBarTitle: string = 'ReLiOx - Gaming Session Manager';
  public sideBarUserPanelTitle: string = 'User Panel';
  public ifUserNotChosen: boolean = false;

  // CRUD objects
  public userPostData: UserPost = new UserPost('', '', 0);

  constructor(private userService: UserService) {}

  public createUser(userPostData: UserPost): UserPost {
    this.userService.POST(userPostData).subscribe({
      next: (createdUser: UserPost) => {
        console.log(createdUser);
      },
      error: (error) => {
        console.error('Error:', error);
      },
      complete: () => {
        console.log('User successfully created!');
      },
    });
    return userPostData;
  }
}
