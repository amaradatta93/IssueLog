import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Issue } from '../models/issue';

@Injectable({
  providedIn: 'root'
})
export class AddIssueService {

  constructor(private httpClient: HttpClient) { }


  addIssues(issue: Issue) {
    let addIssueUrl = 'http://127.0.0.1:5000/add-issue';
    const headers = new HttpHeaders(
      {
          'Content-Type': 'application/json'
      });

    return this.httpClient.post(addIssueUrl, issue, {headers: headers});
  }

}
