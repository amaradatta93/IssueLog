import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { AuthService } from '../services/auth.service';
import { FormValidator } from '../_helpers/validator';


@Component({
  selector: 'app-password-change',
  templateUrl: './password-change.component.html',
  styleUrls: ['./password-change.component.css']
})
export class PasswordChangeComponent extends FormValidator implements OnInit {
  error_message: any;
  success_message: any;

  passwordChangeForm = this.formBuilder.group({
    old_password: ['', Validators.required],
    new_password: ['', Validators.required],
    confirm_password: ['', Validators.required]
  });

  constructor(private formBuilder: FormBuilder,
    private authService: AuthService) {
    super();
  }

  ngOnInit(): void {
    this.error_message;
    this.success_message;
  }

  onPasswordChange() {
    if (this.passwordChangeForm.valid) {
      if (this.passwordChangeForm.value['new_password'] === this.passwordChangeForm.value['confirm_password']) {
        this.authService.passwordChange({
          old_password: this.passwordChangeForm.value['old_password'],
          new_password: this.passwordChangeForm.value['new_password']
        }).subscribe(res => {
          if (res['password_change']) {
            this.success_message = "Password Change Successful";
          } else if (res['error']) {
            this.error_message = res['error']
          }
        })
      } else {
        this.error_message = "Passwords do not match";
      }
    }
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
