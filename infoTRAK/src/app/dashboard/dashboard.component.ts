import { Component, OnInit, Input, OnChanges } from '@angular/core';

import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Issue, DashboardIssues } from '../models/issue';
import { DashboardService } from '../services/dashboard.service';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnChanges {
  issues: DashboardIssues[];
  filterValue = null;
  selectedIssue: Issue;
  issueFile: File;
  blob: Blob;
  search_params: string;

  onChangeStatus(value: any) {
    this.filterValue = value;
  }

  constructor(private dashboardService: DashboardService,
    private activatedRoute: ActivatedRoute,
    private modalService: NgbModal) { }

  ngOnInit(): void {
    this.getIssues();
  }

  ngOnChanges() {
    this.filterValue;
  }

  getIssues(): void {
    this.activatedRoute.queryParams.subscribe((param: any) => {
      this.search_params = param.search_params;
      if (this.search_params) {
        this.dashboardService.getSearchedIssues(this.search_params)
          .subscribe((issues: any) => this.issues = issues.issues);
      } else {
        this.dashboardService.getIssues()
          .subscribe((issues: any) => this.issues = issues.issues);
      }
    });
  }

  getFile(issue_file_name): void {
    this.dashboardService.getIssueFile(issue_file_name)
      .subscribe((data) => {
        this.blob = new Blob([data], { type: 'application/pdf' });
        var downloadURL = window.URL.createObjectURL(data);
        var link = document.createElement('a');
        link.href = downloadURL;
        link.download = issue_file_name;
        link.click();
      });
  }

  openScrollableContent(longContent, issue_id) {
    this.modalService.open(longContent, { scrollable: true });
    this.dashboardService.getSelectedIssue(issue_id)
      .subscribe((selectedIssue: any) => this.selectedIssue = selectedIssue.issue);
  }

}
