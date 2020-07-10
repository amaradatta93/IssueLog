import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filterIssues'
})
export class FilterIssuesPipe implements PipeTransform {

  transform(issues: any, fieldObj: any): unknown {
    let domain = null;

    if(fieldObj){

      if (fieldObj['fleet'] && fieldObj['hos']) {
        domain = 'All';
      }else if (fieldObj['fleet']) {
        domain = 'Fleet';
      } else if (fieldObj['hos']) {
        domain = 'HOS';
      }

      if (domain === 'All') {
        issues = issues;
      } else if (domain) {
        issues = issues.filter(issue => issue['domain'] === domain);
      }

      if (fieldObj['status'] === 'All') {
        issues = issues;
      } else {
        issues = issues.filter(issue => issue['status'] === fieldObj['status']);
      }
    
      return issues;
    } else {
      return issues;
    }

  }
}
