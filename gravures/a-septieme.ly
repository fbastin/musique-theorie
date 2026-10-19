\version "2.24.3"
%% Fichier produit par outils/generer_accords.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  <<
    \new Staff {
      \accidentalStyle forget
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      <g' b' d'' f''>1 <b' d'' f'' g''>1 <d' f' g' b'>1 <f' g' b' d''>1
      \bar "|."
    }
    \addlyrics { \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup \concat { "V" \hspace #0.15 \raise #0.55 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" "5" } } \markup \concat { "V" \hspace #0.15 \raise #0.55 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "4" "3" } } \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "2" } } }
    \addlyrics { "basse : sol" "basse : si" "basse : ré" "basse : fa" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #3.0
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
