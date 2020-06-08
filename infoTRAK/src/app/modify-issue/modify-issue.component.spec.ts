import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifyIssueComponent } from './modify-issue.component';

describe('ModifyIssueComponent', () => {
  let component: ModifyIssueComponent;
  let fixture: ComponentFixture<ModifyIssueComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModifyIssueComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModifyIssueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
