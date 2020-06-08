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
  addIssueForm: FormGroup;

  constructor(private formBuilder: FormBuilder,
    private addIssueService: AddIssueService,
    private router: Router) { }

  ngOnInit(): void {
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
      support_engineer: ['Ravi'],
      issue_fixed_date: [''],
      status: ['Working'],
      support_engineer_comments: [''],
    });

  }

  onSubmit() {
    console.log(this.addIssueForm.value);

    this.addIssueService.addIssues(this.addIssueForm.value).subscribe(res => {
      console.warn('Your issue has been recorded');
      console.log("Response from tasks service: ", res)
      if (res['success'] === true){
        this.router.navigateByUrl('/')
      }
    });
  }

  todayDate() {
    const currentDate = new Date();
    return currentDate.toISOString().substring(0,10);
  }

}
