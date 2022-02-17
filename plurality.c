#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    // ginawa ko lang kay gi compare ko ang number of candidates which is candidate_count
    for (int i = 0; i < candidate_count; i++)
    {
        // tapos i compare mo siya para malaman if siya ba talaga
        if (strcmp(candidates[i].name, name) == 0)
        {
            // then add vote which is .vote ilagay mo
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    // declare a integer
    int maximum_vote = 0;

    // Determine the highest number of votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > maximum_vote)
        {
            // so maging same sila ng maximum votes if greater than
            maximum_vote = candidates[i].votes;
        }
    }
    //identify and print the winner(s)
    for (int i = 0; i < candidate_count; i++)
    {
        // so dito malaman if sino mas higher number kasi yun ang maximum namber oh
        if (candidates[i].votes == maximum_vote)
        {
            printf("%s\n", candidates[i].name);
        }
    }
    return;
}