import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { FormValidator } from '../_helpers/validator';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent extends FormValidator implements OnInit {
  show: boolean = false;
  error_message: any;
  success_message: any;
  buttonName: any = 'Log In';

  logInForm = this.formBuilder.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });


  registerForm = this.formBuilder.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
    email: ['', Validators.required]
  });


  forgotPasswordForm = this.formBuilder.group({
    email_to: ['', Validators.required]
  });

  constructor(private authService: AuthService,
    private formBuilder: FormBuilder,
    private modalService: NgbModal,
    private router: Router) {
    super();
    if (this.authService.currentUserValue) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    this.error_message;
    this.success_message;
  }

  toggle() {
    this.show = !this.show;

    if (this.show) {
      this.buttonName = "Register";
    } else {
      this.buttonName = "Log In";
    }
  }

  onLogin() {
    this.error_message = null;
    this.success_message = null;
    this.authService.logInUser(this.logInForm.value)
      .subscribe(res => {
        if (res['error']) {
          this.error_message = res['error'];
          console.log(res['error']);
          this.router.navigateByUrl('/auth');
        } else if (this.authService.currentUserValue) {
          console.warn('Login successful');
          this.router.navigateByUrl('/');
        }
      });
  }

  onRegister() {
    this.error_message = null;
    this.success_message = null;
    this.authService.registerUser(this.registerForm.value)
    .subscribe(res => {
      if (res['error']) {
        this.error_message = res['error'];
      } else if (res['register'] === true) {
        console.warn('Registration successful');
        this.router.navigateByUrl('/auth');
        this.success_message = 'Successfully registered';
      }
    });
  }

  forgotPassword() {
    this.authService.resetPassword(this.forgotPasswordForm.value)
    .subscribe(res => {
      if (res['error']) {
        this.error_message = res['error'];
        this.forgotPasswordForm.reset();
        this.modalService.dismissAll();
      } else if (res['password_reset'] === true) {
        console.warn('Reset successful');
        this.success_message = `If your Email-ID is registered you should've received the email on ${this.forgotPasswordForm.value.email_to}`;
        this.forgotPasswordForm.reset();
        this.modalService.dismissAll();
      }
    });
  }

  openSm(content) {
    this.modalService.open(content, { centered: true });
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

}
