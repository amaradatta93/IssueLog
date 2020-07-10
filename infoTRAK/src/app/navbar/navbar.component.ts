import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';

import { UserDetails } from '../models/user';
import { AuthService } from '../services/auth.service';
import { NavbarService } from '../services/navbar.service';
import { SupportEngineer } from '../models/support-engineer';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  support_engineers: SupportEngineer[];
  error_message: any;
  success_message: any;
  searchValue: string;
  user: UserDetails;
  @Output() statusUpdate = new EventEmitter();

  addSupportEngineerForm = this.formBuilder.group({
    support_engineer_name: ['']
  });

  filterForm = this.formBuilder.group({
    fleet: [false],
    hos: [false],
    status: ['All']
  });

  constructor(private authService: AuthService,
    private navbarService: NavbarService,
    private modalService: NgbModal,
    private formBuilder: FormBuilder,
    private router: Router) { }

  ngOnInit(): void {
    this.getUser();
    this.error_message;
    this.success_message;
  }

  addFilter() {
    this.statusUpdate.emit(this.filterForm.value);
  }

  getUser() {
    this.navbarService.getUserDetails()
      .subscribe(user => this.user = user)
  }

  logout() {
    this.authService.logOutUser()
      .subscribe(res => {
        console.warn('Logout successful');
        if (res['login'] === false) {
          this.router.navigateByUrl('/auth');
        }
      });
  }

  passwordChange() {
    this.router.navigateByUrl('/settings/password-change');
  }

  openScrollableContent(longContent) {
    this.modalService.open(longContent, { scrollable: true });
    this.getSupportEngineer()
  }

  getSupportEngineer() {
    this.navbarService.getSupportEngineer()
      .subscribe((support_engineers: any) => {
        if (support_engineers) {
          this.support_engineers = support_engineers.support_engineers;
        } else {
          this.support_engineers = null;
        }
      });
  }

  addSupportEngineer() {
    this.navbarService.addSupportEngineer(this.addSupportEngineerForm.value)
      .subscribe(res => {
        if (res['error']) {
          this.error_message = res['error'];
        } else if (res['success'] === true) {
          this.addSupportEngineerForm.reset();
          this.getSupportEngineer()
          this.success_message = "Support engineer added";
        }
      });
  }

  deleteSupportEngineer(id) {
    this.navbarService.deleteSupportEngineer(id)
      .subscribe(res => {
        if (res['error']) {
          this.modalService.dismissAll();
          this.error_message = "Failed to delete the support engineer";
        } else if (res['success'] === true) {
          this.getSupportEngineer();
          this.success_message = "Successfully deleted the support engineer";
        }
      });
  }

  clearMessage() {
    this.error_message = null;
    this.success_message = null;
  }

  clearFilter() {
    location.reload(true);
  }

}
