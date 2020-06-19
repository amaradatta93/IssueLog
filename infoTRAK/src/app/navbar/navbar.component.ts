import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  searchValue: string;
  @Output() statusUpdate = new EventEmitter();

  constructor(private authService: AuthService,
    private router: Router) { }

  ngOnInit(): void {

  }

  selected(event, value: any) {
    this.statusUpdate.emit(value);
  }

  logout() {
    this.authService.logOutUser()
    .subscribe(res => {
      console.warn('Logout successful');
      console.log("Response from tasks service: ", res)
      if (res['login'] === false){
        this.router.navigateByUrl('/auth')
      }
    });
  }

}
