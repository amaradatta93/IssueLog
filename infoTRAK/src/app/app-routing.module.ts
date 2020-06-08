import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { AddIssueComponent } from './add-issue/add-issue.component';
import { ModifyIssueComponent } from './modify-issue/modify-issue.component';


const routes: Routes = [
  {path: '', component: DashboardComponent},
  {path: 'add-issue', component: AddIssueComponent},
  {path: 'modify-issue/:id', component: ModifyIssueComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
