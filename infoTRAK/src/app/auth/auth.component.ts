import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { FormValidator } from '../_helpers/validator';

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

  constructor(private authService: AuthService,
    private formBuilder: FormBuilder,
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
        console.warn('Login successful');
        if (this.authService.currentUserValue) {
          this.router.navigateByUrl('/');
        } else {
          this.error_message = res['error'];
          this.router.navigateByUrl('/auth');
        }
      });
  }

  onRegister() {
    this.error_message = null;
    this.success_message = null;
    this.authService.registerUser(this.registerForm.value)
      .subscribe(res => {
        console.warn('Registration successful');
        if (res['register'] === true) {
          this.router.navigateByUrl('/auth');
          this.success_message = 'Successfully registered';
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
