import { Component, OnInit, Input, OnChanges } from '@angular/core';

import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Issue } from '../models/issue';
import { DashboardService } from '../services/dashboard.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnChanges {
  issues: Issue[];
  search_params: string;
  filterValue = null;

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

  openScrollableContent(longContent) {
    this.modalService.open(longContent, { scrollable: true });
  }

}
