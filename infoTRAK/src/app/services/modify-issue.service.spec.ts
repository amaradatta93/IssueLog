import { TestBed } from '@angular/core/testing';

import { ModifyIssueService } from './modify-issue.service';

describe('ModifyIssueService', () => {
  let service: ModifyIssueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModifyIssueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
