import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { map } from 'rxjs/operators';
import { BehaviorSubject, Observable } from 'rxjs';

import { Register, User } from '../models/user';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser: Observable<User>;


  constructor(private httpClient: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  registerUser(registeration_details: Register): Observable<any> {
    let registerUrl = `http://127.0.0.1:5000/auth/register`;
    return this.httpClient.post(registerUrl, registeration_details)
  }

  logInUser(login_details: User): Observable<any> {
    let logInUrl = `http://127.0.0.1:5000/auth/login`;
    return this.httpClient.post(logInUrl, login_details)
      .pipe(map((user: any) => {
        if (user['token'] !== null) {
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentUserSubject.next(user);
          return user;
        } else {
          location.reload(true);
        }
      }));
  }

  logOutUser(): Observable<any> {
    let logOutUrl = `http://127.0.0.1:5000/auth/logout`;
    return this.httpClient.get<any>(logOutUrl)
      .pipe(map((res: any) => {
        if (res['login'] === false) {
          localStorage.removeItem('currentUser');
          this.currentUserSubject.next(null);
          return res;
        }
      }
    ));
  }

}
