import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';

import { Observable, throwError, from } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

import{ AuthService } from '../services/auth.service'

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService,
    private router: Router) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
            if (err.status === 401) {
                this.authService.logOutUser();
                this.router.navigateByUrl('/auth');
            }

            const error = err.error.message || err.statusText;
            return throwError(error);
        }))
    }

}
