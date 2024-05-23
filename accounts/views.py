from utils import generate_activation_code

class Register(View):
    template_name = "user/register.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
     #Registering a users and make them temporal
    def post(self, request, *args, **kwargs):
        
        email_address = request.POST.get("email_address")
        password = request.POST.get("password")
        
        if len(password) < 4:
            messages.error(request, "Password Must be at least 4 characters")
            return redirect(request.META.get("HTTP_REFERER"))
        
        # Validate email address format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format")
            return redirect(request.META.get("HTTP_REFERER"))

        
        if User.objects.filter(email_address=email_address):
            messages.error(request, "Email Already Exist")
            return redirect(request.META.get("HTTP_REFERER"))
        
        if CodeEmail.objects.filter(email_address=email_address):
            code_user = CodeEmail.objects.get(email_address=email_address)
            generated_code = generate_activation_code()
            code_user.code = generated_code
            code_user.save()
            context = {
            "generated_code": generated_code,
            }
            html_message = render_to_string("user/verify.html",context)
            plain_message = strip_tags(html_message)
            try:
                message = EmailMultiAlternatives(
                subject="Email Verification Code",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_address],
            )
                message.attach_alternative(html_message, 'text/html')
                message.send()
                messages.success(request, "Email Verification Code Sent to Email")
                return redirect("users:verify")
            except Exception as e:
                messages.error(request,f"Error sending email: {e}, try again")
                return redirect(request.META.get("HTTP_REFERER"))
        
        # Generate Verification Code
        generated_code = generate_activation_code()
        context = {
            "generated_code": generated_code,
        }
        html_message = render_to_string("user/verify.html",context)
        plain_message = strip_tags(html_message)
        
        code_user = CodeEmail.objects.create(email_address=email_address, password=password,code=generated_code)
        code_user.save()
        # Send Email with verification Code  to User Email 
        try:
            message = EmailMultiAlternatives(
            subject="Email Verification Code",
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email_address],
            )
            message.attach_alternative(html_message, 'text/html')
            message.send()
            messages.success(request, "Email Verification Code Sent to Email")
            return redirect("users:verify")
        except Exception as e:
            messages.error(request,f"Error sending email: {e}, try again")
            return redirect(request.META.get("HTTP_REFERER"))
    
        return render(request, self.template_name)



class CodeVerificationView(View):
    template_name = "user/code_verification.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    #Verifying users account to make it permanent
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code") # 262626626
    
        # Check if code is not numeric
        if not code.isdigit():
            messages.error(request, "The code must be numeric")
            return redirect(request.META.get("HTTP_REFERER"))
        try:
            code_email = CodeEmail.objects.get(code=code) # object
            user = User.objects.create_user(username=code_email.email_address, email_address=code_email.email_address, password=code_email.password)
            user.save()
            user = authenticate(request, email_address=code_email.email_address, password=code_email.password)
            if user is not None:
                login(request,user)
                code_email.delete()
                messages.success(request, "Email Verified")
                return redirect('files:user-dashboard')
            else:
                return redirect('/')
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid or Wrong Code Entered")
            return redirect(request.META.get("HTTP_REFERER"))

        return render(request, self.template_name)
