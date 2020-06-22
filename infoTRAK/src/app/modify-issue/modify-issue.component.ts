import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Issue } from '../models/issue';
import { ModifyIssueService } from '../services/modify-issue.service';


@Component({
  selector: 'app-modify-issue',
  templateUrl: './modify-issue.component.html',
  styleUrls: ['./modify-issue.component.css']
})
export class ModifyIssueComponent implements OnInit {
  issue: Issue;
  issue_id: number;
  error_message: any;
  success_message: any;
  editIssueForm: FormGroup;


  constructor(private modifyIssueService: ModifyIssueService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.error_message;
    this.success_message;
    this.activatedRoute.paramMap.subscribe((param: any) => {
      this.issue_id = param.params.id
      this.modifyIssueService.getIssue(this.issue_id)
        .subscribe((issue: any) => {
        this.issue = issue.issue;
          this.editIssueForm = this.formBuilder.group({
            customer_name: [this.issue.customer_name],
            company: [this.issue.company],
            source: [this.issue.source],
            e_mail: [this.issue.email],
            phone_number: [this.issue.phone],
            issue_report_date: [this.issue.issue_report_date],
            issue_description: [this.issue.issue_description],
            domain: [this.issue.domain],
            priority: [this.issue.priority],
            assigned_to: [this.issue.assigned_to],
            issue_fixed_date: [this.issue.issue_fix_date],
            status: [this.issue.status],
            support_engineer_comments: [this.issue.support_engineer_comments]
          });
        });
    })


  }

  onSubmit() {
    this.modifyIssueService.updateIssue(this.issue_id, this.editIssueForm.value)
    .subscribe(res => {
      console.warn('Your issue has been updated');
      if (res['success'] === true){
        this.success_message = 'Issue Update Successful';
        this.router.navigateByUrl('/')
      } else {
        this.error_message = res['error'];
      }
    });
  }

  onSubmitDelete() {
    this.modifyIssueService.deleteIssue(this.issue_id)
    .subscribe(res => {
      console.warn('Your issue has been deleted');
      if (res['success'] === true){
        this.router.navigateByUrl('/')
      } else {
        this.error_message = res['error'];
      }
    });
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
