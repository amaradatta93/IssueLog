import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { HttpClient } from '@angular/common/http';

import { DashboardIssues, Issue } from '../models/issue';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private httpClient: HttpClient) {}

  getIssues(): Observable<DashboardIssues[]> {
    let dashboardUrl = 'http://127.0.0.1:5000/';
    return this.httpClient.get<DashboardIssues[]>(dashboardUrl);
  }

  getSearchedIssues(search_param: string): Observable<DashboardIssues[]> {
    let searchIssueUrl = `http://127.0.0.1:5000/search?search_param=${search_param}`;
    return this.httpClient.get<DashboardIssues[]>(searchIssueUrl);
  }

  getSelectedIssue(issue_id): Observable<Issue> {
    let selectecIssueUrl = `http://127.0.0.1:5000/${issue_id}`;
    return this.httpClient.get<Issue>(selectecIssueUrl);
  }

}
