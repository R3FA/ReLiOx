import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserPost } from '../model/Users/UserPostModel';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private baseURL: string = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  public POST(userObject: UserPost): Observable<UserPost> {
    return this.http.post<UserPost>(
      `${this.baseURL}/users/`,
      userObject.toFlaskFormat()
    );
  }
}
