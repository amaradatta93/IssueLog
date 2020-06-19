import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  show: boolean = false;
  error_message: any;
  success_message: any;
  buttonName: any = 'Log In';

  logInForm = this.formBuilder.group({
    username: [''],
    password: ['']
  });


  registerForm = this.formBuilder.group({
    username: [''],
    password: [''],
    email: ['']
  });

  constructor(private authService: AuthService,
    private formBuilder: FormBuilder,
    private router: Router) {
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
    this.authService.logInUser(this.logInForm.value)
      .subscribe(res => {
        console.warn('Login successful');
        console.log("Response from tasks service: ", res)
        if (this.authService.currentUserValue) {
          this.router.navigateByUrl('/');
        } else {
          this.error_message = res['error'];
          console.log(this.error_message)
          this.router.navigateByUrl('/auth');
        }
      });
  }

  onRegister() {
    this.authService.registerUser(this.registerForm.value)
      .subscribe(res => {
        console.warn('Registration successful');
        console.log("Response from tasks service: ", res)
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
