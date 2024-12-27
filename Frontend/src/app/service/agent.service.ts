import { Injectable } from '@angular/core';
import { AgentGet, AgentPost } from '../model/Agent/AgentPostModel';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AgentService {
  private baseURL: string = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  public Create(userObject: AgentPost): Observable<AgentGet> {
    return this.http.post<AgentGet>(
      `${this.baseURL}/agent-session/`,
      userObject
    );
  }
}
