from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Issue
from .serializers import IssueSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
import re

class IssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    filter_backends = [SearchFilter]
    
    # This enables native ?search=keyword functionality across these fields
    search_fields = ['title', 'description', 'labels']

    def get_queryset(self):
        # Default sort by newest first
        queryset = Issue.objects.all().order_by('-last_updated')
        
        # Custom filter to handle ?difficulty=Easy/Medium/Hard
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty__iexact=difficulty)
            
        return queryset

@api_view(['GET'])
def issue_stats(request):
    issues = Issue.objects.all()
    
    # 1. Pie Chart Distribution
    distribution = {
        'Easy': issues.filter(difficulty='Easy').count(),
        'Medium': issues.filter(difficulty='Medium').count(),
        'Hard': issues.filter(difficulty='Hard').count(),
    }
    
    # 2. Word Cloud Generation
    # We strip out common stop words to make the clouds meaningful
    stop_words = {'the', 'a', 'to', 'and', 'is', 'in', 'it', 'of', 'for', 'this', 'that', 'on', 'with', 'as', 'we', 'are', 'be', 'can', 'not', 'have', 'from', 'but'}
    word_clouds = {'Easy': [], 'Medium': [], 'Hard': []}
    
    for diff in ['Easy', 'Medium', 'Hard']:
        # Combine all titles and descriptions for this difficulty
        text = " ".join([i.title + " " + (i.description or "") for i in issues.filter(difficulty=diff)])
        # Extract words longer than 2 characters
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        filtered_words = [w for w in words if w not in stop_words]
        
        # Get the top 20 most common words
        most_common = Counter(filtered_words).most_common(20)
        word_clouds[diff] = [{'text': word, 'value': count} for word, count in most_common]
        
    return Response({
        'distribution': distribution,
        'word_clouds': word_clouds
    })        