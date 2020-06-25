import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Issue } from '../models/issue';
import { ModifyIssueService } from '../services/modify-issue.service';
import { DashboardService } from '@app/services/dashboard.service';


@Component({
  selector: 'app-modify-issue',
  templateUrl: './modify-issue.component.html',
  styleUrls: ['./modify-issue.component.css']
})
export class ModifyIssueComponent implements OnInit {
  issue: Issue;
  issue_id: number;
  issueFile: File;
  blob: Blob;
  error_message: any;
  success_message: any;
  editIssueForm: FormGroup;


  constructor(private modifyIssueService: ModifyIssueService,
    private dashboardService: DashboardService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.error_message;
    this.success_message;
    this.issueFile = null;

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
          issue_file: [],
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
    const myFormValue = this.editIssueForm.value
    let myFormValueKeys = Object.keys(myFormValue);

    const myFormData = new FormData();
    for (let i = 0; i < myFormValueKeys.length; i++) {
      let key = myFormValueKeys[i];

      if (key === 'issue_file') {
        if (this.issueFile) {
          myFormData.append('issue_file', this.issueFile, this.issueFile.name);
        } else {
          myFormData.append('issue_file', '');
        }
      } else {
        myFormData.append(key, myFormValue[key]);
      }
    }

    this.modifyIssueService.updateIssue(this.issue_id, myFormData)
      .subscribe(res => {
        if (res['success'] === true) {
          console.warn('Your issue has been updated');
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
        if (res['success'] === true) {
          this.router.navigateByUrl('/')
        } else {
          this.error_message = res['error'];
        }
      });
  }

  handleFileInput(files: FileList) {
    this.issueFile = files.item(0);
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

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
