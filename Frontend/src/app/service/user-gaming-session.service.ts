import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { DailyObligationGetFlaskFormat } from '../model/DailyObligation/DailyObligationGetModel';
import { Observable } from 'rxjs';
import { GamingSessionPostFlaskFormat } from '../model/GamingSession/GamingSessionPostModel';
import {
  GamingSessionGetFlaskFormat,
  GamingSessionsDeleteParameters,
  GamingSessionsGetParameters,
} from '../model/GamingSession/GamingSessionGetModel';

@Injectable({
  providedIn: 'root',
})
export class UserGamingSessionService {
  private baseURL: string = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  // DailyObligation
  public GetAll(): Observable<DailyObligationGetFlaskFormat[]> {
    return this.http.get<DailyObligationGetFlaskFormat[]>(
      `${this.baseURL}/daily-obligations/`
    );
  }

  // GamingSession
  public GetAllSessions(
    params: GamingSessionsGetParameters
  ): Observable<GamingSessionGetFlaskFormat[]> {
    return this.http.get<GamingSessionGetFlaskFormat[]>(
      `${this.baseURL}/user-gaming-session/${params.eventDate}/${params.userID}`
    );
  }

  public Create(
    userID: number,
    session: GamingSessionPostFlaskFormat
  ): Observable<GamingSessionPostFlaskFormat> {
    return this.http.post<GamingSessionPostFlaskFormat>(
      `${this.baseURL}/user-gaming-session/${userID}`,
      session
    );
  }

  public Delete(params: GamingSessionsDeleteParameters): Observable<void> {
    return this.http.delete<void>(
      `${this.baseURL}/user-gaming-session/${params.sessionID}/${params.userID}`
    );
  }
}
