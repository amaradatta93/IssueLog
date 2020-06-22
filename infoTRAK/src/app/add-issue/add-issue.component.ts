import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, FormBuilder } from '@angular/forms';

import { AddIssueService } from '../services/add-issue.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-issue',
  templateUrl: './add-issue.component.html',
  styleUrls: ['./add-issue.component.css']
})
export class AddIssueComponent implements OnInit {
  error_message: any;
  success_message: any;
  addIssueForm: FormGroup;

  constructor(private formBuilder: FormBuilder,
    private addIssueService: AddIssueService,
    private router: Router) { }

  ngOnInit(): void {
    this.error_message = null;
    this.success_message = null;
    this.addIssueForm = this.formBuilder.group({
      customer_name: [''],
      company: [''],
      source: ['Phone'],
      e_mail: [''],
      phone_number: [''],
      issue_report_date: [this.todayDate()],
      issue_description: [''],
      domain: ['Fleet'],
      priority: ['Low'],
      assigned_to: ['Support'],
      issue_fixed_date: [''],
      status: ['Working'],
      support_engineer_comments: [''],
    });

  }

  onSubmit() {
    this.addIssueService.addIssues(this.addIssueForm.value).subscribe(res => {
      console.warn('Your issue has been recorded');
      if (res['success'] === true){
        this.success_message = "Issue Added Successfully";
        this.router.navigateByUrl('/')
      } else {
        this.error_message = res['error'];
      }
    });
  }

  todayDate() {
    const currentDate = new Date();
    return currentDate.toISOString().substring(0,10);
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
