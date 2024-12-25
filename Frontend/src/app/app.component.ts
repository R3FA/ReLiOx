import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [CommonModule],
})
export class AppComponent {
  public navBarTitle: string = 'ReLiOx - Gaming Session Manager';
  public sideBarUserPanelTitle: string = 'User Panel';
  public ifUserNotChosen: boolean = true;
}
