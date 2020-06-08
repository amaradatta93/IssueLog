import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';

import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Issue } from '../models/issue';

@Injectable({
  providedIn: 'root'
})
export class ModifyIssueService {
  hearders;

  constructor(private httpClient: HttpClient) {}

  getIssue(issue_id): Observable<Issue[]> {
    let issueUrl = `http://127.0.0.1:5000/${issue_id}`;
    return this.httpClient.get<Issue[]>(issueUrl);
  }
  
  headers = new HttpHeaders(
    {
        'Content-Type': 'application/json'
    });

  updateIssue(issue_id, updatedIssue: Issue) {
    let updateIssueUrl = `http://127.0.0.1:5000/edit/${issue_id}`;
    return this.httpClient.put(updateIssueUrl, updatedIssue, {headers: this.headers})
  }

  deleteIssue(issue_id: number) {
    let deleteIssueUrl = `http://127.0.0.1:5000/delete/${issue_id}`;
    return this.httpClient.delete(deleteIssueUrl, {headers: this.headers});
  }

}
