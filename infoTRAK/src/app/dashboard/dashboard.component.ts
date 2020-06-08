import { Component, OnInit } from '@angular/core';

import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Issue } from '../models/issue';
import { DashboardService } from '../services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  issues: Issue[];

  constructor(private dashboardService: DashboardService,
      private modalService: NgbModal) { }

  ngOnInit(): void {
    this.getIssues();
  }

  getIssues(): void {
    this.dashboardService.getPosts()
    .subscribe((issues: any) => this.issues = issues.issues);
  }

  openScrollableContent(longContent) {
    this.modalService.open(longContent, { scrollable: true });
  }

}
