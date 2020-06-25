import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AddIssueService {

  constructor(private httpClient: HttpClient) { }

  addIssues(issue: FormData) {
    let addIssueUrl = 'http://127.0.0.1:5000/add-issue';
    return this.httpClient.post(addIssueUrl, issue);
  }

}
