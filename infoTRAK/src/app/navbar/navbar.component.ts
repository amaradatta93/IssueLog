import { Component, OnInit, Output, EventEmitter } from '@angular/core';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  searchValue: string;
  @Output() statusUpdate = new EventEmitter();

  constructor() { }

  ngOnInit(): void {

  }

  selected(event, value: any) {
    this.statusUpdate.emit(value);
  }

}
