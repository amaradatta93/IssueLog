import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filterIssues'
})
export class FilterIssuesPipe implements PipeTransform {

  transform(issues: any, fieldObj: any): unknown {

    if (fieldObj) {
      let field = fieldObj["field"];
      let fieldValue = fieldObj["fieldValue"];
      return issues.filter(issue => issue[field] === fieldValue);
    } else {
      return issues;
    }
  }

}
