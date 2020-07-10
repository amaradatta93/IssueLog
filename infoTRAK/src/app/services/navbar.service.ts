import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { UserDetails } from '../models/user';
import { SupportEngineer } from '../models/support-engineer';

@Injectable({
  providedIn: 'root'
})
export class NavbarService {

  constructor(private httpClient: HttpClient) { }

  getUserDetails(): Observable<UserDetails> {
    let userDetailUrl =  `http://127.0.0.1:5000/auth/user`;
    return this.httpClient.get<UserDetails>(userDetailUrl);
  }

  getSupportEngineer(): Observable<SupportEngineer[]> {
    let getEngineerUrl =  `http://127.0.0.1:5000/support-engineers/`;
    return this.httpClient.get<SupportEngineer[]>(getEngineerUrl);
  }

  addSupportEngineer(name: any): Observable<any> {
    let addEngineerUrl = `http://127.0.0.1:5000/support-engineers/add`;
    return this.httpClient.post(addEngineerUrl, name);
  }

  deleteSupportEngineer(id: any): Observable<any> {
    let deleteEngineerUrl = `http://127.0.0.1:5000/support-engineers/delete/${id}`;
    return this.httpClient.delete(deleteEngineerUrl);
  }

}
