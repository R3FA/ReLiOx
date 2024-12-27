import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserPostFlaskFormat } from '../model/Users/UserPostModel';
import { UserGetFlaskFormat } from '../model/Users/UserGetModel';
import { UserPatchFlaskFormat } from '../model/Users/UserPatchModel';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private baseURL: string = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  public GetAll(): Observable<UserGetFlaskFormat[]> {
    return this.http.get<UserGetFlaskFormat[]>(`${this.baseURL}/users/`);
  }

  public Create(
    userObject: UserPostFlaskFormat
  ): Observable<UserPostFlaskFormat> {
    return this.http.post<UserPostFlaskFormat>(
      `${this.baseURL}/users/`,
      userObject
    );
  }

  public Patch(
    id: number,
    user: UserPatchFlaskFormat
  ): Observable<UserPatchFlaskFormat> {
    return this.http.patch<UserPatchFlaskFormat>(
      `${this.baseURL}/users/${id}`,
      user
    );
  }

  public Delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseURL}/users/${id}`);
  }
}
