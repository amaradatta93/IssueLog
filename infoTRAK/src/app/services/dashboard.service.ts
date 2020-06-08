import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { HttpClient } from '@angular/common/http';

import { Issue } from '../models/issue';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) {}

  private dashboardUrl = 'http://127.0.0.1:5000/';

  getPosts(): Observable<Issue[]> {
    return this.http.get<Issue[]>(this.dashboardUrl);
  }
}
