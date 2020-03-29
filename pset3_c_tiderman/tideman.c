#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (vote(j, name, ranks) == false)
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }
    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks.
void record_preferences(int ranks[])
{
    // Increases the preferences by one as
    // preferences[i][j] should represent the number of voters
    // who prefer candidate i over candidate j.
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int pair = 0;
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair].winner = i;
                pairs[pair].loser = j;
                pair++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair].winner = j;
                pairs[pair].loser = i;
                pair++;
            }
        }
    }

    // Save the number of pairs into the global variable.
    pair_count = pair;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{

    int strength1 = -1;
    int strength2 = -1;

    pair temp_pair;

    bool completed = false;
    while (completed == false)
    {
        completed = true;
        for (int i = 0; i < pair_count - 1; i++)
        {
            strength1 = preferences[pairs[i].winner][pairs[i].loser];
            strength2 = preferences[pairs[i + 1].winner][pairs[i + 1].loser];

            // Swapping the pairs if the strength of the second
            // is bigger than the strengh of the first.
            if (strength1 < strength2)
            {
                printf("Swapping\n");
                temp_pair = pairs[i];
                pairs[i] = pairs[i + 1];
                pairs[i + 1] = temp_pair;
                completed = false;
            }
        }
    }
}

// Checks if there is cycle between winner and looser
bool has_cycle(int winner, int loser)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i] == true)
        {
            has_cycle(i, winner);
            return true;
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;

        if (has_cycle(winner, loser) == false)
        {
            locked[winner][loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    // Finds the first candidate that doesn't
    // have any inbound arrows.
    bool has_inbound;
    bool has_outbound;
    int winner = -1;

    for (int i = 0; i < candidate_count; i++)
    {
        has_inbound = false;
        has_outbound = false;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == true)
            {
                has_inbound = true;
            }

            if (locked[i][j] == true)
            {
                has_outbound = true;
            }
        }

        if (has_inbound == false && has_outbound == true)
        {
            winner = i;
            break;
        }
    }

    // Prints out the winner
    printf("%s\n", candidates[winner]);
}
