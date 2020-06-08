import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { HttpClient } from '@angular/common/http';

import { Issue } from '../models/issue';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) {}

  getIssues(): Observable<Issue[]> {
    let dashboardUrl = 'http://127.0.0.1:5000/';
    return this.http.get<Issue[]>(dashboardUrl);
  }

  getSearchedIssues(search_param: string): Observable<Issue[]> {
    let searchIssueUrl = `http://127.0.0.1:5000/search?search_param=${search_param}`;
    return this.http.get<Issue[]>(searchIssueUrl);
  }
}
