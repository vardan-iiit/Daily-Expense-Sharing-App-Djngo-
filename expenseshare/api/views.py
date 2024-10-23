from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action   
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        participants = data.get('participants')
        print(participants)
        split_method = data.get('split_method')
        split_details= []
        total_amount = float(data.get('amount'))
        
        
        if split_method == 'equal':
            
            num_participants = len(participants)
            equal_share = total_amount / num_participants
            
            data['split_details'] = [{'user_id': user, 'amount': equal_share} for user in participants]
        
        elif split_method == 'exact':
            
            data['split_details'] = data.get('split_details')  # Already provided in the request

        elif split_method == 'percentage':
            percentages = data.get('split_details')
           
            total_percentage = sum(percentages)
          
            if total_percentage != 100:
                return Response({'error': 'Percentages must add up to 100%'}, status=status.HTTP_400_BAD_REQUEST)
            data['split_details'] = [{'user_id': i, 'amount': (total_amount * p) / 100} for p, i in zip(percentages, participants)]

      
        data.pop('participants', None)

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            expense = serializer.save()

            if participants:
                expense.participants.set(participants)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get_user_expenses(self, request, user_id):
        expenses = Expense.objects.filter(participants__id=user_id)
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)
    
    def overall_expenses(self, request):
        expenses = Expense.objects.all()
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='balancesheet')
    def download_balance_sheet(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.pdf"'
        
        p = canvas.Canvas(response)
        p.drawString(100, 750, "Balance Sheet")
        
        # Query all expenses
        expenses = Expense.objects.all()
        
        y_position = 720  # Starting position for writing
        
        for expense in expenses:
            # Print the expense details
            p.drawString(100, y_position, f"Expense: {expense.description}")
            p.drawString(100, y_position - 15, f"Amount: {expense.amount}")
            
            # Retrieve and print participants
            
         
            
            
            
          
            
            # Move y_position down for the next expense
            y_position -= 60
            
            # If y_position is too low, create a new page
            if y_position < 100:
                p.showPage()  # Save the current page
                y_position = 750  # Reset y_position for the new page
        
        p.showPage()  # Save the final page
        p.save()  # Finalize the PDF
        
        return response
