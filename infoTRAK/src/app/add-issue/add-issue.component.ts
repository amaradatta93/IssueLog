import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AddIssueService } from '../services/add-issue.service';
import { NavbarService } from '../services/navbar.service';
import { FormValidator } from '../_helpers/validator';

import { SupportEngineer } from '../models/support-engineer';
import { UserDetails } from '../models/user';

@Component({
  selector: 'app-add-issue',
  templateUrl: './add-issue.component.html',
  styleUrls: ['./add-issue.component.css']
})
export class AddIssueComponent extends FormValidator implements OnInit {
  error_message: any;
  success_message: any;
  issueFile: File;
  addIssueForm: FormGroup;
  user: UserDetails;
  support_engineers: SupportEngineer[];

  constructor(private formBuilder: FormBuilder,
    private addIssueService: AddIssueService,
    private navbarService: NavbarService,
    private router: Router) {
      super();
    }

  ngOnInit(): void {
    this.error_message = null;
    this.success_message = null;
    this.issueFile = null;
    this.getSupportEngineers();
    this.getUser();

    this.addIssueForm = this.formBuilder.group({
      customer_name: ['', Validators.required],
      company: ['', Validators.required],
      source: ['Phone'],
      e_mail: ['', Validators.required],
      phone_number: ['', Validators.required],
      issue_report_date: [this.todayDate()],
      issue_description: ['', Validators.required],
      issue_file: [''],
      domain: ['Fleet'],
      priority: ['Low'],
      assigned_to: ['Support'],
      support_engineer: ['unassigned'],
      issue_fixed_date: ['', Validators.required],
      status: ['Working'],
      support_engineer_comments: ['']
    });

  }

  getUser() {
    this.navbarService.getUserDetails()
      .subscribe(user => this.user = user)
  }

  getSupportEngineers () {
    this.navbarService.getSupportEngineer()
      .subscribe((support_engineers: any) => {
        if (support_engineers) {
          this.support_engineers = support_engineers.support_engineers;
        } else {
          this.support_engineers = null;
        }
      });
  }

  onSubmit() {
    const myFormValue = this.addIssueForm.value
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

    this.addIssueService.addIssues(myFormData).subscribe(res => {
      if (res['success'] === true) {
        console.warn('Your issue has been recorded');
        this.success_message = "Issue Added Successfully";
        this.router.navigateByUrl('/')
      } else {
        this.error_message = res['error'];
      }
    });
  }

  todayDate() {
    const currentDate = new Date();
    return currentDate.toISOString().substring(0, 10);
  }

  handleFileInput(files: FileList) {
    this.issueFile = files.item(0);
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
