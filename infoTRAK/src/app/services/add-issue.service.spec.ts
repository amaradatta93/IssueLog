import { TestBed } from '@angular/core/testing';

import { AddIssueService } from './add-issue.service';

describe('AddIssueService', () => {
  let service: AddIssueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AddIssueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
