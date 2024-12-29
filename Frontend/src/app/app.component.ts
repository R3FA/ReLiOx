import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { UserPost } from './model/Users/UserPostModel';
import { UserService } from './service/user.service';
import { FormsModule } from '@angular/forms';
import { UserGet, UserGetFlaskFormat } from './model/Users/UserGetModel';
import { UserPostFlaskFormat } from './model/Users/UserPostModel';
import { UserPatch, UserPatchFlaskFormat } from './model/Users/UserPatchModel';
import {
  DailyObligationGet,
  DailyObligationGetFlaskFormat,
} from './model/DailyObligation/DailyObligationGetModel';
import { UserGamingSessionService } from './service/user-gaming-session.service';
import {
  FatigueLevel,
  GamingSessionPostFlaskFormat,
  StressLevel,
} from './model/GamingSession/GamingSessionPostModel';
import {
  GamingSessionGet,
  GamingSessionGetFlaskFormat,
  GamingSessionsDeleteParameters,
  GamingSessionsGetParameters,
} from './model/GamingSession/GamingSessionGetModel';
import { Agent, AgentGet } from './model/Agent/AgentPostModel';
import { AgentService } from './service/agent.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [DatePipe],
  imports: [CommonModule, FormsModule],
})
export class AppComponent implements OnInit {
  // HTML Titles
  public navBarTitle: string = 'ReLiOx - Gaming Session Manager';
  public navBarAgentButtonTitle: string = ' Summon Agent';
  public sideBarUserPanelTitle: string = 'User Panel';
  public sideBarChooseUserTitle: string = 'Choose';
  public formNicknameTitle: string = 'Nickname';
  public formEmailTitle: string = 'Email';
  public formAgeTitle: string = 'Age';
  public createGameSessionButtionTitle: string = 'Create Gaming Session';
  public currentUser: string = '';
  public cardSessionEventDate: string = 'Event Date';
  public cardSessionStartTime: string = 'Start time';
  public cardSessionEndTime: string = 'End time';
  public cardSessionFatigueLevel: string = 'Fatigue level';
  public cardSessionStressLevel: string = 'Stress level';
  public cardSessionDailyObligations: string = 'Daily obligations';
  public agentMessage: string = 'No messages yet';

  // Bool
  public isUserChosen: boolean = false;
  public areSessionsEmpty: boolean = true;

  // CRUD objects
  public userGetAllData: UserGet[] = [];
  public userPostData: UserPostFlaskFormat = new UserPostFlaskFormat('', '', 0);
  public userPatchData: UserPatch = new UserPatch(0, '', '', 0);
  public userData: UserGet = new UserGet(0, '', '', 0);

  public dailyObligationsData: DailyObligationGet[] = [];

  public fatigueLevels: FatigueLevel[] = Object.values(FatigueLevel);
  public stressLevels: StressLevel[] = Object.values(StressLevel);
  public userGamingSessionPostData: GamingSessionPostFlaskFormat =
    new GamingSessionPostFlaskFormat(0, '', '', '', []);
  public userGamingSessionGetParams: GamingSessionsGetParameters =
    new GamingSessionsGetParameters('', 0);
  public userGamingSessionsData: GamingSessionGet[] = [];
  public userGamingSessionDeleteParams: GamingSessionsDeleteParameters =
    new GamingSessionsDeleteParameters(0, 0);

  // Response types
  public userDeleteAlertType: 'success' | 'danger' | null = null;
  public userDeleteAlertMessage: string = '';

  public userCreateAlertType: 'success' | 'danger' | null = null;
  public userCreateAlertMessage: string = '';

  public sessionCreateAlertType: 'success' | 'danger' | null = null;
  public sessionCreateAlertMessage: string = '';

  public sessionGetAlertType: 'success' | 'danger' | null = null;
  public sessionGetAlertMessage: string = '';

  public sessionDeleteAlertType: 'success' | 'danger' | null = null;
  public sessionDeleteAlertMessage: string = '';

  public agentPostAlertType: 'success' | 'danger' | null = null;
  public agentPostAlertMessage: string = '';

  constructor(
    private userService: UserService,
    private userGamingSessionService: UserGamingSessionService,
    private agentService: AgentService
  ) {}

  ngOnInit(): void {
    this.GetAllUsers();
  }

  public refreshPage(): void {
    setTimeout(() => {
      window.location.reload();
    }, 2000);
  }

  public closeButton(): void {
    this.userDeleteAlertType = null;
    this.userCreateAlertType = null;
    this.sessionCreateAlertType = null;
    this.userDeleteAlertMessage = '';
    this.userCreateAlertMessage = '';
    this.sessionCreateAlertMessage = '';
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
    this.currentUser = `User: ${this.userData.getUserNickname()}`;
    this.isUserChosen = true;
  }

  public loadDailyObligations(): DailyObligationGet[] {
    this.userGamingSessionService.GetAll().subscribe({
      next: (sessions: DailyObligationGetFlaskFormat[]) => {
        this.dailyObligationsData = sessions.map(
          (session) =>
            new DailyObligationGet(
              session.id,
              session.daily_obligation_type.replace('DailyObligation.', '')
            )
        );
      },
      error: (error) => {
        console.error(error?.error?.message);
      },
    });
    return [];
  }

  public setGamingSessionPostData(): void {
    this.userGamingSessionPostData.user_id = this.userData.getUserID();
  }

  public GetUsersGamingSessions(): GamingSessionGet[] {
    this.userGamingSessionGetParams.userID = this.userData.getUserID();

    if (this.userGamingSessionGetParams.eventDate == '') {
      return [];
    }

    this.userGamingSessionService
      .GetAllSessions(this.userGamingSessionGetParams)
      .subscribe({
        next: (sessions: GamingSessionGetFlaskFormat[]) => {
          this.userGamingSessionsData = sessions.map(
            (session) =>
              new GamingSessionGet(
                session.id,
                session.user_id,
                session.event_date,
                session.fatigue_level.replace('FatigueLevel.', ''),
                session.stress_level.replace('StressLevel.', ''),
                session.daily_obligations
              )
          );
        },
        error: (error) => {
          this.userCreateAlertType = 'danger';
          this.userCreateAlertMessage =
            error?.error?.message || 'An error occurred!';
        },
        complete: () => {
          if (this.userGamingSessionsData.length == 0)
            this.areSessionsEmpty = true;
          else this.areSessionsEmpty = false;
        },
      });
    return [];
  }

  public CreateGamingSession(
    userID: number,
    session: GamingSessionPostFlaskFormat
  ): void {
    this.userGamingSessionService.Create(userID, session).subscribe({
      next: () => {
        this.sessionCreateAlertType = 'success';
        this.sessionCreateAlertMessage = `Gaming session for ${this.currentUser} has been CREATED successfully!`;
        this.refreshPage();
      },
      error: (error) => {
        this.sessionCreateAlertType = 'danger';

        const errorMessage = error?.error?.message;

        if (errorMessage) {
          if (typeof errorMessage === 'object') {
            const firstKey = Object.keys(errorMessage)[0];
            this.sessionCreateAlertMessage =
              errorMessage[firstKey] || 'An error occurred!';
          } else {
            this.sessionCreateAlertMessage =
              errorMessage || 'An error occurred!';
          }
        } else {
          this.sessionCreateAlertMessage = 'An error occurred!';
        }
      },
    });
  }

  public DeleteUserGamingSession(session: GamingSessionGet): void {
    this.userGamingSessionDeleteParams.setSessionID(session.id);
    this.userGamingSessionDeleteParams.setUserID(session.userID);

    this.userGamingSessionService
      .Delete(this.userGamingSessionDeleteParams)
      .subscribe({
        next: () => {
          this.sessionDeleteAlertType = 'success';
          this.sessionDeleteAlertMessage = `Gaming Session for ${this.currentUser} has been deleted successfully!`;
          this.refreshPage();
        },
        error: (error) => {
          this.sessionDeleteAlertType = 'danger';
          this.sessionDeleteAlertMessage =
            error?.error?.message || 'An error occurred!';
        },
      });
  }

  // Agent Endpoint

  public PrepareAgentData(session: GamingSessionGet): void {
    let agentPostData = new Agent(
      session.fatigueLevel,
      session.stressLevel,
      session.dailyObligations.map((obligation) =>
        obligation.daily_obligation_type.replace('DailyObligation.', '')
      )
    );

    console.log(agentPostData);
    this.PredictSessionDuration(agentPostData);
  }

  public PredictSessionDuration(agentPostData: Agent): void {
    this.agentService.Create(agentPostData).subscribe({
      next: (agentMessage: AgentGet) => {
        this.agentMessage = agentMessage.predicted_session_duration;
      },
      error: (error) => {
        this.agentPostAlertType = 'danger';
        this.agentPostAlertMessage =
          error?.error?.message || 'An error occurred!';
      },
    });
  }
}
