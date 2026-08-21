// LLVM pass that uses ML-based heuristics for loop unrolling
// TODO: currently using simple heuristics, need to integrate actual ML model

#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Analysis/ScalarEvolution.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/Pass.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Utils/LoopUtils.h"

using namespace llvm;

namespace {

struct MLUnrollPass : public PassInfoMixin<MLUnrollPass> {
    
    // extract features from a loop (simplified version of what we do in Python)
    struct LoopFeatures {
        unsigned num_instructions = 0;
        unsigned num_loads = 0;
        unsigned num_stores = 0;
        unsigned num_branches = 0;
        unsigned trip_count = 0;
        bool has_constant_trip_count = false;
    };
    
    LoopFeatures extractFeatures(Loop *L) {
        LoopFeatures features;
        
        // count instructions in loop blocks
        for (BasicBlock *BB : L->blocks()) {
            for (Instruction &I : *BB) {
                features.num_instructions++;
                
                if (isa<LoadInst>(I)) {
                    features.num_loads++;
                } else if (isa<StoreInst>(I)) {
                    features.num_stores++;
                } else if (isa<BranchInst>(I)) {
                    features.num_branches++;
                }
            }
        }
        
        return features;
    }
    
    // simple heuristic based on our ML findings
    // TODO: replace with actual model prediction
    bool shouldUnroll(const LoopFeatures &features) {
        // heuristic based on our benchmarks:
        // - small instruction count is good
        // - too many memory ops is bad
        // - small trip count is good
        
        if (features.num_instructions < 20) {
            // small loop body, probably benefits
            return true;
        }
        
        if (features.num_instructions > 100) {
            // too large, code bloat risk
            return false;
        }
        
        // check memory intensity
        unsigned memory_ops = features.num_loads + features.num_stores;
        float memory_ratio = (float)memory_ops / features.num_instructions;
        
        if (memory_ratio > 0.5) {
            // memory-bound, unrolling won't help much
            return false;
        }
        
        // default: let LLVM decide
        return true;
    }
    
    PreservedAnalyses run(Function &F, FunctionAnalysisManager &FAM) {
        auto &LI = FAM.getResult<LoopAnalysis>(F);
        
        errs() << "MLUnrollPass analyzing function: " << F.getName() << "\n";
        
        unsigned loop_count = 0;
        unsigned should_unroll_count = 0;
        
        // iterate through all loops
        for (Loop *L : LI) {
            loop_count++;
            
            LoopFeatures features = extractFeatures(L);
            bool unroll_decision = shouldUnroll(features);
            
            if (unroll_decision) {
                should_unroll_count++;
            }
            
            errs() << "  Loop " << loop_count << ": ";
            errs() << features.num_instructions << " instructions, ";
            errs() << features.num_loads << " loads, ";
            errs() << features.num_stores << " stores";
            errs() << " -> " << (unroll_decision ? "UNROLL" : "SKIP") << "\n";
        }
        
        errs() << "  Total: " << loop_count << " loops, ";
        errs() << should_unroll_count << " marked for unrolling\n";
        
        // for now we just analyze, don't actually modify
        // TODO: integrate with UnrollLoop() to actually apply the transformation
        
        return PreservedAnalyses::all();
    }
};

} // anonymous namespace

// plugin registration
extern "C" LLVM_ATTRIBUTE_WEAK PassPluginLibraryInfo llvmGetPassPluginInfo() {
    return {
        LLVM_PLUGIN_API_VERSION, "MLUnrollPass", LLVM_VERSION_STRING,
        [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                    if (Name == "ml-unroll") {
                        FPM.addPass(MLUnrollPass());
                        return true;
                    }
                    return false;
                }
            );
        }
    };
}
