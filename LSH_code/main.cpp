#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <map>
#include <iomanip>

#include <boost/filesystem.hpp>
#include <boost/mpi.hpp>

#include "fastq_reader.h"
#include "nethub.h"
#include "config.h"
#include "kmer_count_map.h"
#include "kmer_ext_map.h"
#include "contig.h"
#include "utils.h"
#include "lsh.h"
#include "contig_store.h"
#include "kmer_contig_map.h"
#include "iostream"
#include <stdio.h>
using namespace std;
namespace mpi = boost::mpi;
namespace fs  = boost::filesystem;


#define KMER_BUFFER_SIZE 1024
#define KMER_TAG 0
#define KMER_SIZE_TAG 1
#define DONE_TAG 2

#define LSH_ON 1

#define LOAD_FROM_UFX 0
#define HASH_SIZE 12289
static const k_t k = 76; // Config::K;
static const int q_min = 19; // Config::K;

int get_kmer_bin(qekmer_t* qekmer, k_t k, int world_size)
{
#if LSH_ON
    //cout << k ;
    size_t hash = lsh(qekmer->kmer, k);
#else
    size_t hash = kmer_hash(0, qekmer->kmer, k);
#endif
    //printf("world_size: %d\n",world_size);
    printf("GeneId ID: %s",qekmer->id);
    printf("Node_ID: %d\n",hash%HASH_SIZE);
    return hash % world_size;
    //return hash % HASH_SIZE;
}

/* Checks to see if the qekmer meets the criteria to being sent. For example,
 * this function checks to make sure that the kmer does not contain an 'N'
 * anywhere in the kmer.
 */
bool check_qekmer_qual(qekmer_t* qekmer, k_t k)
{
    //if (qekmer->lqual <= Config::Q_MIN && qekmer->rqual <= Config::Q_MIN)
    //if (qekmer->lqual <= q_min && qekmer->rqual <= q_min)
    //    return false;

    return true;
}

/* Sets the qekmer to the canonical qekmer. */
void canonize_qekmer(qekmer_t* qekmer, k_t k)
{
    kmer_a revcmp[kmer_size(k)];
    //cout << "<<< " << qekmer->kmer << ">>>" << k << "\n" ;
    revcmp_kmer(revcmp, qekmer->kmer, k);
    if (cmp_kmer(qekmer->kmer, revcmp, k) > 0) {
        memcpy(qekmer->kmer, revcmp, kmer_size(k));
        qual_t tmp_qual = qekmer->lqual;
        base tmp_ext = inv_base((base) qekmer->exts.left);
        qekmer->lqual = qekmer->rqual;
        qekmer->exts.left = inv_base((base) qekmer->exts.right);
        qekmer->rqual = tmp_qual;
        qekmer->exts.right = tmp_ext;
    }
}

FastQReader* get_reader(int argc, char* argv[], mpi::communicator& world, k_t k)
{
    vector<string> fnames;
    for (int i = 0; i < argc; ++i) {
        fnames.push_back(string(argv[i]));
    }

    FastQReader* reader = new FastQReader(fnames, k);
    uintmax_t offset = reader->total_bytes() / world.size() * world.rank();
    reader->seek(offset);
    reader->set_max_byte(offset + reader->total_bytes() / world.size());

    return reader;
}

void build_store(FastQReader* r, KmerCountMap& kmer_count_map, mpi::communicator& world)
{
    NetHub nethub(world, qekmer_size(k));

    bool node_done[world.size()]; // Stores the non-blocking receive requests
    for (int i = 0; i < world.size(); i++) {
        node_done[i] = false;
    }
    bool done_reading = false;
    bool all_done = false;

    qekmer_t* send_qekmer = (qekmer_t*) malloc(qekmer_size(k));
    qekmer_t* recv_qekmer = (qekmer_t*) malloc(qekmer_size(k));

    while (!all_done) {
        if (r->read_next(send_qekmer)) {
	     cout << "reading next left:" << send_qekmer->lqual << "right:" << send_qekmer->rqual << " \n" << endl;
	    //cout << send_qekmer->kmer.size << "\n" ;
            if (check_qekmer_qual(send_qekmer, k)) {
                //canonize_qekmer(send_qekmer, k);
		cout << "\n--------------------------------\n" ;

		//cout <<  send_qekmer->kmer << "\n";

                //int node_id = get_kmer_bin(send_qekmer, k, 1000);
                int node_id = get_kmer_bin(send_qekmer, k, world.size());
		//printf( "node_id: %d\n", node_id);// "\n";
		//cout << send_qekmer->kmer << "\n";
		cout << "********************************" ;
                nethub.send(node_id, send_qekmer);
            }
        } else {
	    cout << "nothing to read\n" ;
            if (!done_reading) {
                nethub.done();
                done_reading = true;
            }
        }

        all_done = true;
        for (int i = 0; i < world.size(); i++)
        {
            if (node_done[i]) continue;

            int status;
            while ((status = nethub.recv(i, recv_qekmer)) == 0) {
                kmer_count_map.insert(recv_qekmer);
            }

            if (status == 1)
                node_done[i] = true;
            else
                all_done = false;
        }
    }

    free(send_qekmer);
    free(recv_qekmer);
}

void print_ufxs(const char* outprefix, KmerExtMap& kmer_ext_map, int rank)
{
    stringstream ss;
    ss << outprefix << ".ufx." << rank;
    FILE* outfile = fopen(ss.str().c_str(), "w");
    if (outfile == NULL)
        panic("Could not open file: %s\n", ss.str().c_str());
    kmer_ext_map.print_ufxs(outfile);
    fclose(outfile);
}


void print_contigs(char* outprefix, ContigStore& contig_store, int rank)
{
    stringstream ss;
    ss << outprefix << ".contig." << rank;
    FILE* outfile = fopen(ss.str().c_str(), "w");
    if (outfile == NULL)
        panic("Could not open file: %s\n", ss.str().c_str());
    contig_store.fprint_contigs(outfile);
    fclose(outfile);
}

void print_contigs(char* outprefix, KmerContigMap& kmer_contig_map, int rank)
{
    stringstream ss;
    ss << outprefix << ".contig." << rank;
    FILE* outfile = fopen(ss.str().c_str(), "w");
    if (outfile == NULL)
        panic("Could not open file: %s\n", ss.str().c_str());
    kmer_contig_map.fprint_contigs(outfile);
    fclose(outfile);
}



int main(int argc, char* argv[])
{
    mpi::environment env(argc, argv);
    mpi::communicator world;

    if (argc < 3) {
        printf("main_lsh outfile infile...\n");
        exit(1);
    }

    Config::load_config("mermaid.conf");

    //if (world.rank() == 0)
    //{
    //    printf("PID %d on %d ready for attach\n", getpid(), world.rank());
    //    fflush(stdout);
    //    volatile int i = 0;
    //    while (0 == i)
    //        sleep(5);
    //}

    /* =======================
     * Phase 1: k-mer counting
     * ======================= */
    KmerExtMap* kmer_ext_map = new KmerExtMap(k);
    KmerCountMap* kmer_count_map = new KmerCountMap(k);


    FastQReader* reader = get_reader(argc - 2, &argv[2], world, k);
    build_store(reader, *kmer_count_map, world);
    kmer_count_map->trim(*kmer_ext_map);
    delete kmer_count_map;
    //print_ufxs(argv[1], *kmer_ext_map, world.rank());

    return 0;
}
